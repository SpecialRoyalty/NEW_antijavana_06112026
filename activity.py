"""Per-opening participation snapshots; no dependence on deleted chat history."""

async def record_activity(db,user_id,session):
    await db.execute('''INSERT INTO member_activity(user_id,opening_serial,message_count)
      VALUES($1,$2,1) ON CONFLICT(user_id,opening_serial)
      DO UPDATE SET message_count=member_activity.message_count+1''',user_id,session)


async def inactive_candidates(db,session,after=0,limit=200):
    return await db.fetch('''SELECT m.user_id,m.joined_at,w.warned_serial,w.eligible
       FROM members m LEFT JOIN member_activity a
         ON a.user_id=m.user_id AND a.opening_serial=$1
       LEFT JOIN inactivity_warnings w ON w.user_id=m.user_id
       WHERE m.left_at IS NULL AND m.joined_at IS NOT NULL
         AND COALESCE(a.message_count,0)=0 AND m.removed_flag=false
         AND m.user_id>$2 ORDER BY m.user_id LIMIT $3''',session,after,limit)


async def record_warning(db,user_id,session,eligible):
    await db.execute('''INSERT INTO inactivity_warnings(user_id,warned_serial,eligible,warned_at)
       VALUES($1,$2,$3,now()) ON CONFLICT(user_id) DO UPDATE SET
       warned_serial=EXCLUDED.warned_serial,eligible=EXCLUDED.eligible,warned_at=now()''',
       user_id,session,eligible)


async def clear_warning(db,user_id):
    await db.execute('DELETE FROM inactivity_warnings WHERE user_id=$1',user_id)


#
# @print_run_seconds
# def update_data(table, old_val=999, new_val=888):
#     result = 0
#     if not table or not isinstance(table, str):
#         return result
#     else:
#         cls_name = ''
#         if table.upper() == 'Session_Activity'.upper():
#             cls_name = SessionActivity
#             sql_update = 'update session_activity set session_id=%d, course_id=%d, lesson_id=%d where session_id=%d and course_id=%d and lesson_id=%d' % (
#                 new_val,new_val,new_val, old_val,old_val,old_val)
#             # cls_update = SessionActivity.query.filter_by(session_id=old_val, course_id=old_val, lesson_id=old_val).all()
#             # cls_update.update(commit=False, dict(session_id=old_val, course_id=old_val, lesson_id=old_val))
#         elif table.upper() == 'Session_Activity_Pk'.upper():
#             cls_name = SessionActivityPk
#             sql_update = 'update session_activity_pk set session_activity_id=:session_activity_id, score=:score, max_combo=:max_combo where session_activity_id=:session_activity_id and score=:score and max_combo=:max_combo' ,{
#                 "session_activity_id": new_val,
#                 "score": new_val,
#                 "max_combo": new_val,
#                 "session_activity_id": old_val,
#                 "score": old_val,
#                 "max_combo": old_val
#             }
#
#         if cls_name:
#             try:
#                 result = db.engine.execute(sql_update)
#             except Exception,ex:
#                 print Exception,':',ex
#             finally:
#                 pass
#             return result


        #
        #     fields = dict(zip(keys, row))
        #
        #     stat_school = StatSchools.query.filter_by(school_id=fields['school_id']).first()
        #     if stat_school:
        #         fields['updated_at'] = dt.datetime.now()
        #         stat_school.update(commit=False, **fields)
        #
        # db.session.commit()

# @print_run_seconds
# def delete_data(table, val=999):
#     result = 0
#     if not table or not isinstance(table, str):
#         return result
#     else:
#         cls_name = cls_data = ''
#         if table.upper() == 'Session_Activity'.upper():
#             cls_name = SessionActivity
#             cls_data = session_activity_data
#         elif table.upper() == 'Session_Activity_Pk'.upper():
#             cls_name = SessionActivityPk
#             cls_data = session_activity_pk_data
#         if not(cls_name and cls_data): return result
#
#     for i in range(records):
#         try:
#             db.session.add(cls_name.create(**cls_data))
#             db.session.commit()
#             result += 1
#         except Exception,ex:
#             print Exception,':',ex
#         finally:
#             pass
#     return result
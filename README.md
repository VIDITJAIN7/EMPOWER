add any errors or required edits here!! <br>
error in db_empower() func, not yet identified <br>
issue in dataytypeof aadhar and contact, reports out of range value - i have changed those to numeric but i think char could be better<br>
there's an issue in update:<br>
    update_query = f'UPDATE empmaster SET {field_to_update} = %s WHERE empid = %s'<br>
    cur1.execute(update_query, (updated_value, employee_id))<br>
i think a condition would need to be added so that for numeric datatype columns you simply type in set <> = <>, but for the rest quotes would have been used.
but there might be some other error also since it is not working for even aadhar at my end.
also while adding records, gender being set is M even if F is selected.

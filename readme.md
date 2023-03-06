##### **Here is the Postgres function for searching text**


`
CREATE OR REPLACE FUNCTION searchText(my_substring text)
RETURNS TABLE (matched_element text)
AS $$
BEGIN
    RETURN QUERY
    select matched_cols from (
        SELECT unnest("page-content") as matched_cols FROM "pageContent" WHERE user_id = 1 
    ) subquery
    where LOWER(matched_cols) like '%' || my_substring || '%';
END;
$$ LANGUAGE plpgsql;
`


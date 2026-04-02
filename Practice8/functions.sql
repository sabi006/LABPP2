-- Поиск
CREATE OR REPLACE FUNCTION get_contacts_by_pattern(p TEXT)
RETURNS TABLE(contact_name TEXT, contact_phone TEXT) AS $$
BEGIN
    RETURN QUERY
    SELECT c.name AS contact_name,
           c.phone AS contact_phone
    FROM contacts c
    WHERE c.name ILIKE '%' || p || '%'
       OR c.phone ILIKE '%' || p || '%';
END;
$$ LANGUAGE plpgsql;


-- Пагинация
CREATE OR REPLACE FUNCTION get_contacts_paginated(p_limit INT, p_offset INT)
RETURNS TABLE(contact_name TEXT, contact_phone TEXT) AS $$
BEGIN
    RETURN QUERY
    SELECT c.name AS contact_name,
           c.phone AS contact_phone
    FROM contacts c
    LIMIT p_limit OFFSET p_offset;
END;
$$ LANGUAGE plpgsql;
"CREATE TABLE urls
(
    id bigint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1 ),
    name character varying(255) NOT NULL,
    created_at date,
    CONSTRAINT urls_pkey PRIMARY KEY (id)
);"

"CREATE TABLE url_checks
(
    id bigint NOT NULL,
    url_id bigint,
    status_code bigint,
    h1 text,
    title text,
    description text,
    created_at date NOT NULL,
    CONSTRAINT url_checks_pkey PRIMARY KEY (id)
);"


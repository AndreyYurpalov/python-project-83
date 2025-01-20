CREATE TABLE IF NOT EXISTS new_urls
(
    id bigint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1 ),
    name character varying(255) COLLATE pg_catalog."default" NOT NULL,
    created_at date NOT NULL,
    CONSTRAINT new_name_pkey PRIMARY KEY (id)
)


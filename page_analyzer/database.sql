-- Table: public.urls

-- DROP TABLE IF EXISTS public.urls;

CREATE TABLE IF NOT EXISTS public.urls
(
    id bigint NOT NULL,
    name text COLLATE pg_catalog."default" NOT NULL,
    created_at time without time zone NOT NULL,
    CONSTRAINT urls_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.urls
    OWNER to postgres;

COMMENT ON TABLE public.urls
    IS 'urls с полями id, name и created_at';
-- Table: public.GTV

-- DROP TABLE IF EXISTS public."GTV";

CREATE TABLE IF NOT EXISTS public."GTV"
(
    "RECORD_PRIMARY_ID" character varying COLLATE pg_catalog."default" NOT NULL,
    "DATE_TIMESTAMP" character varying COLLATE pg_catalog."default",
    "BARCODE_READ" character varying COLLATE pg_catalog."default",
    "BARCODE_NUMBER" character varying COLLATE pg_catalog."default",
    "BARCODE_IMAGE" character varying COLLATE pg_catalog."default",
    "GTV_READ" character varying COLLATE pg_catalog."default",
    "PROCESSED_IMAGE" character varying COLLATE pg_catalog."default",
    "OVERALL_STATUS" character varying[] COLLATE pg_catalog."default",
    CONSTRAINT "GTV_pkey" PRIMARY KEY ("RECORD_PRIMARY_ID")
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public."GTV"
    OWNER to postgres;
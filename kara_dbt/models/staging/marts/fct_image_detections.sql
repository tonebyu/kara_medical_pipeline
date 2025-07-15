{{ config(materialized='table') }}

SELECT
    message_id,
    detected_object_class,
    confidence_score,
    image_file
FROM {{ source('staging', 'fct_image_detections') }}

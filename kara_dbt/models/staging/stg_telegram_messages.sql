with source as (
    select * from raw.telegram_messages
),

renamed as (
    select
        id as message_id,
        timestamp as message_timestamp,
        timestamp::date as date,
        message_text as message,
        null::bigint as channel_id,  -- placeholder; replace if you have real channel_id data
        length(message_text) as message_length,
        false as has_image  -- assuming no media column
    from source
)

select * from renamed

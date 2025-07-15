select
  message_id,
  channel_id,
  date::date as date_id,
  message_length,
  has_image
from {{ ref('stg_telegram_messages') }}

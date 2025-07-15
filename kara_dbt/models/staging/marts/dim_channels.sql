select
  distinct channel_id
from {{ ref('stg_telegram_messages') }}

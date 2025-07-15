select *
from {{ ref('stg_telegram_messages') }}
where message is null or message = ''

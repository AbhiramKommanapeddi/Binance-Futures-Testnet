import time
from bot.orders import OrderManager
from bot.logging_config import logger

class TWAPStrategy:
    def __init__(self, order_manager: OrderManager):
        self.order_manager = order_manager

    def execute(self, symbol, side, total_quantity, duration_minutes, num_chunks):
        chunk_qty = total_quantity / num_chunks
        interval_seconds = (duration_minutes * 60) / num_chunks
        
        logger.info(f"Starting TWAP: {side} {total_quantity} {symbol} over {duration_minutes}m in {num_chunks} chunks")
        
        for i in range(num_chunks):
            logger.info(f"TWAP Chunk {i+1}/{num_chunks}: Placing Market Order for {chunk_qty}")
            try:
                self.order_manager.place_market_order(symbol, side, chunk_qty)
            except Exception as e:
                logger.error(f"TWAP Chunk {i+1} failed: {e}")
            
            if i < num_chunks - 1:
                logger.info(f"Waiting {interval_seconds} seconds for next chunk...")
                time.sleep(interval_seconds)
        
        logger.info("TWAP Strategy completed.")

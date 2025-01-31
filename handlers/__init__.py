from aiogram import Router
from .basic_commands import router as basic_router
from .training_handlers import router as training_router
from .cards_handlers import router as cards_router
from .add_card_handlers import router as add_card_router
from .reset_handlers import router as reset_router

router = Router()
router.include_router(basic_router)
router.include_router(training_router)
router.include_router(cards_router)
router.include_router(add_card_router)
router.include_router(reset_router)

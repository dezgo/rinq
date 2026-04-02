"""
Pluggable integration interfaces for Tina/Rinq.

Each interface defines what Tina needs from an external system.
Implementations live in subpackages (e.g. watson/ for bot-team).

Usage:
    from rinq.integrations import get_staff_directory, get_ticket_service
    staff = get_staff_directory()
    people = staff.get_active_staff()
"""

import logging
from typing import Optional

logger = logging.getLogger(__name__)

# Singleton instances — set during app initialization
_staff_directory = None
_ticket_service = None
_permission_service = None
_customer_lookup = None
_order_lookup = None
_email_service = None
_ai_receptionist = None


def init_integrations(provider: str = 'watson', **kwargs):
    """Initialize all integration services for the given provider.

    Args:
        provider: Which integration provider to use ('watson' for bot-team)
    """
    global _staff_directory, _ticket_service, _permission_service
    global _customer_lookup, _order_lookup, _email_service, _ai_receptionist

    if provider == 'watson':
        from rinq.integrations.watson import (
            WatsonStaffDirectory,
            WatsonTicketService,
            WatsonPermissionService,
            WatsonCustomerLookup,
            WatsonOrderLookup,
            WatsonEmailService,
            WatsonAIReceptionist,
        )
        _staff_directory = WatsonStaffDirectory()
        _ticket_service = WatsonTicketService()
        _permission_service = WatsonPermissionService()
        _customer_lookup = WatsonCustomerLookup()
        _order_lookup = WatsonOrderLookup()
        _email_service = WatsonEmailService()
        _ai_receptionist = WatsonAIReceptionist()
        logger.info("Integrations initialized: watson (bot-team)")
    else:
        raise ValueError(f"Unknown integration provider: {provider}")


def get_staff_directory():
    """Get the staff directory integration."""
    return _staff_directory


def get_ticket_service():
    """Get the ticket service integration."""
    return _ticket_service


def get_permission_service():
    """Get the permission service integration."""
    return _permission_service


def get_customer_lookup():
    """Get the customer lookup integration."""
    return _customer_lookup


def get_order_lookup():
    """Get the order lookup integration."""
    return _order_lookup


def get_email_service():
    """Get the email service integration."""
    return _email_service


def get_ai_receptionist():
    """Get the AI receptionist integration."""
    return _ai_receptionist

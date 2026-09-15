"""
Notification handler for Agentic Advisor
For MVP: stores notifications in memory/logs
Can be extended to Firebase/Twilio/WhatsApp later
"""

import logging
from typing import Dict, List
from datetime import datetime
from .schemas import AgentNotification, AgentAction

logger = logging.getLogger(__name__)


class NotificationStore:
    """
    Simple in-memory notification store
    In production, this would be a database
    """
    
    def __init__(self):
        self._notifications: Dict[str, List[AgentNotification]] = {}
    
    def add(self, notification: AgentNotification):
        """Add a notification"""
        farm_id = notification.farm_id
        
        if farm_id not in self._notifications:
            self._notifications[farm_id] = []
        
        self._notifications[farm_id].append(notification)
        logger.info(f"Notification added for {farm_id}: {notification.action} - {notification.message}")
    
    def get_latest(self, farm_id: str) -> AgentNotification:
        """Get latest notification for a farm"""
        if farm_id not in self._notifications or not self._notifications[farm_id]:
            return None
        
        return self._notifications[farm_id][-1]
    
    def get_all(self, farm_id: str) -> List[AgentNotification]:
        """Get all notifications for a farm"""
        return self._notifications.get(farm_id, [])


# Global notification store
notification_store = NotificationStore()


class Notifier:
    """
    Notification handler
    
    For MVP: logs and stores in memory
    Can be extended for real notification channels:
    - SMS (Twilio)
    - WhatsApp
    - Firebase Push Notifications
    - Email
    """
    
    def __init__(self):
        self.store = notification_store
    
    def create_notification(
        self,
        farm_id: str,
        action: AgentAction,
        message: str,
        priority: str
    ) -> AgentNotification:
        """
        Create and store a notification
        
        Args:
            farm_id: Farm identifier
            action: Action taken
            message: Farmer-friendly message
            priority: Priority level
            
        Returns:
            Created notification
        """
        notification = AgentNotification(
            farm_id=farm_id,
            action=action,
            message=message,
            priority=priority,
            created_at=datetime.now()
        )
        
        # Store notification
        self.store.add(notification)
        
        # Log for MVP
        logger.info(
            f"[{priority}] Notification for {farm_id}: "
            f"{action.value} - {message}"
        )
        
        # In production, send to external channels:
        # self._send_sms(farm_id, message)
        # self._send_push(farm_id, message, priority)
        # self._send_whatsapp(farm_id, message)
        
        return notification
    
    def get_latest_notification(self, farm_id: str) -> AgentNotification:
        """Get latest notification for a farm"""
        return self.store.get_latest(farm_id)
    
    def _send_sms(self, farm_id: str, message: str):
        """Placeholder for SMS sending"""
        # Integration with Twilio would go here
        pass
    
    def _send_push(self, farm_id: str, message: str, priority: str):
        """Placeholder for push notification"""
        # Integration with Firebase would go here
        pass
    
    def _send_whatsapp(self, farm_id: str, message: str):
        """Placeholder for WhatsApp message"""
        # Integration with WhatsApp Business API would go here
        pass


# Global notifier instance
notifier = Notifier()

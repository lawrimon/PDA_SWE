import React, { useRef, useEffect } from 'react';
import './Notification.css';

const NotificationPopup = ({ message, onClose }) => {
        return (
          <div className="notification-popup">
            <div className="notification-popup__content">
              <div className="notification-popup__message">{message}</div>
              <button className="notification-popup__close" onClick={onClose}>
                Close
              </button>
            </div>
          </div>
        );
      };

export default NotificationPopup;

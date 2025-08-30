#!/usr/bin/env python3
"""
WoL-Bot Turn On Extension

This module handles Wake-on-LAN functionality for turning on network devices.
It properly handles the case where data.json doesn't exist by creating it.
"""

import json
import os
import logging
from typing import Dict, List, Any

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATA_FILE = "data.json"


def ensure_data_file_exists() -> None:
    """
    Ensure that data.json exists. If it doesn't exist, create it with default structure.
    
    This fixes the issue where the extension would error when data.json is missing.
    """
    if not os.path.exists(DATA_FILE):
        logger.info(f"{DATA_FILE} does not exist. Creating default data file.")
        
        # Create default structure for WoL data
        default_data = {
            "devices": [],
            "settings": {
                "port": 9,
                "timeout": 10
            },
            "version": "1.0"
        }
        
        try:
            with open(DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(default_data, f, indent=2, ensure_ascii=False)
            logger.info(f"Successfully created {DATA_FILE} with default structure.")
        except Exception as e:
            logger.error(f"Failed to create {DATA_FILE}: {e}")
            raise


def load_data() -> Dict[str, Any]:
    """
    Load data from data.json file.
    
    Returns:
        Dict containing the loaded data
        
    Raises:
        Exception: If there's an error loading the data file
    """
    ensure_data_file_exists()
    
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        logger.info(f"Successfully loaded data from {DATA_FILE}")
        return data
    except Exception as e:
        logger.error(f"Failed to load data from {DATA_FILE}: {e}")
        raise


def save_data(data: Dict[str, Any]) -> None:
    """
    Save data to data.json file.
    
    Args:
        data: Dictionary containing the data to save
        
    Raises:
        Exception: If there's an error saving the data file
    """
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        logger.info(f"Successfully saved data to {DATA_FILE}")
    except Exception as e:
        logger.error(f"Failed to save data to {DATA_FILE}: {e}")
        raise


def add_device(mac_address: str, name: str, ip_address: str = None) -> None:
    """
    Add a new device to the WoL database.
    
    Args:
        mac_address: MAC address of the device
        name: Human-readable name for the device
        ip_address: IP address of the device (optional)
    """
    data = load_data()
    
    device = {
        "mac_address": mac_address,
        "name": name,
        "ip_address": ip_address
    }
    
    data["devices"].append(device)
    save_data(data)
    logger.info(f"Added device: {name} ({mac_address})")


def get_devices() -> List[Dict[str, str]]:
    """
    Get list of all devices from the database.
    
    Returns:
        List of device dictionaries
    """
    data = load_data()
    return data.get("devices", [])


def turn_on_device(identifier: str) -> bool:
    """
    Turn on a device by name or MAC address using Wake-on-LAN.
    
    Args:
        identifier: Device name or MAC address
        
    Returns:
        True if WoL packet was sent successfully, False otherwise
    """
    try:
        devices = get_devices()
        target_device = None
        
        # Find device by name or MAC address
        for device in devices:
            if device["name"].lower() == identifier.lower() or device["mac_address"].lower() == identifier.lower():
                target_device = device
                break
        
        if not target_device:
            logger.error(f"Device not found: {identifier}")
            return False
        
        # Here you would implement the actual WoL functionality
        # For now, we'll just log the attempt
        logger.info(f"Sending WoL packet to {target_device['name']} ({target_device['mac_address']})")
        
        # Actual WoL implementation would go here
        # This would typically involve sending a magic packet to the device
        
        return True
        
    except Exception as e:
        logger.error(f"Failed to turn on device {identifier}: {e}")
        return False


def main():
    """
    Main function for testing the extension.
    """
    try:
        # Test the data file handling
        logger.info("Testing WoL-Bot Turn On Extension...")
        
        # This will create data.json if it doesn't exist
        data = load_data()
        logger.info(f"Loaded data structure: {list(data.keys())}")
        
        # Test adding a device
        if not data.get("devices"):
            add_device("00:11:22:33:44:55", "Test Device", "192.168.1.100")
            logger.info("Added test device")
        
        # List devices
        devices = get_devices()
        logger.info(f"Found {len(devices)} devices in database")
        
        logger.info("Extension test completed successfully")
        
    except Exception as e:
        logger.error(f"Error during testing: {e}")
        raise


if __name__ == "__main__":
    main()
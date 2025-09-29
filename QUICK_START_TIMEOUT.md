# Quick Start: Timeout-Based Scanning

## What Changed?

The fingerprint scanner now uses a **5-second timeout** instead of adaptive polling:
- ✅ Scans for 5 seconds
- ⏸️ Pauses after timeout
- ⌨️ Restarts automatically when you press any key

## Quick Setup

### 1. Default Configuration (Recommended)
No configuration needed! The defaults work for most users:
- 5-second timeout
- 0.5-second polling interval
- Automatic keyboard detection

### 2. Custom Configuration (Optional)

Create or edit: `/etc/python-validity/config.ini`

```ini
[scanning]
# How long to scan before pausing (seconds)
scan_timeout = 5.0

# How often to check for fingerprint (seconds)
poll_interval = 0.5

[logging]
# Set to DEBUG to see detailed logs
level = INFO
```

### 3. Restart Service

```bash
sudo systemctl restart python3-validity
```

## Common Scenarios

### Lock Screen
1. Lock screen and walk away
2. Come back, press any key
3. Fingerprint detection starts automatically
4. Place finger to unlock

### Sudo Commands
1. Run `sudo command`
2. Fingerprint detection starts (10 seconds)
3. Either:
   - Use fingerprint within 10 seconds, OR
   - Start typing password (detection pauses)
4. Next sudo command restarts detection

### Multiple Attempts
1. First try: 10 seconds to use fingerprint
2. Timeout: Detection pauses
3. Press any key: Detection restarts for another 10 seconds

## Customization Examples

### Longer Timeout (Patient Users)
```ini
[scanning]
scan_timeout = 15.0
```

### Shorter Timeout (Battery Saving)
```ini
[scanning]
scan_timeout = 5.0
poll_interval = 1.0
```

### Faster Response
```ini
[scanning]
scan_timeout = 10.0
poll_interval = 0.3
```

## Troubleshooting

### Detection Doesn't Restart
**Problem**: Pressing keys doesn't restart detection

**Fix**: Check service logs
```bash
journalctl -u python3-validity -f
```

### Timeout Too Short/Long
**Problem**: Detection pauses too quickly or waits too long

**Fix**: Adjust `scan_timeout` in config file

### High CPU Usage
**Problem**: Service uses too much CPU

**Fix**: Increase `poll_interval` to 1.0 or higher

## Testing

Test the new behavior:
```bash
cd /home/www/DEV-trunk/python-validity
./test_timeout_scanning.py
```

## More Information

See full documentation: `TIMEOUT_BASED_SCANNING.md`

## Key Benefits

- 🔋 **Lower power usage** - No scanning when idle
- 🎯 **Predictable behavior** - Clear 10-second timeout
- ⌨️ **Smart restart** - Automatically resumes on keyboard input
- 🚀 **Simpler config** - Just 2 main settings vs 7+ before

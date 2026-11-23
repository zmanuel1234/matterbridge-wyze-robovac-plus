# Sends the vacuum back to its dock.
from wyze_auth import run, fail, cli, find_vacuum_mac
from getVacuumStatus import work_status


def main(args):
    if len(args) != 1:
        fail("USAGE: vacuumStopSweep.py robovac_nickname")
    nickname = args[0]

    def body(client):
        from wyze_sdk.models.devices import VacuumMode

        device_mac = find_vacuum_mac(client, nickname)
        vacuum = client.vacuums.info(device_mac=device_mac)
        # Mode IDLE is also a vacuum on standby in a room (for example left paused for a
        # while): only Wyze's work status, or charging, says that it is on the dock.
        if work_status(vacuum) == "DOCKED" or (vacuum.mode == VacuumMode.IDLE and vacuum.is_charging):
            fail("RoboVac is already docked....")
        client.vacuums.dock(device_mac=device_mac, device_model=vacuum.product.model)
        print("Vacuum successfully sent back to charge....")

    run(body)


if __name__ == "__main__":
    cli(main)

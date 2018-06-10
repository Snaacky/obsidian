import keyboard
import pymem
import pymem.process

dwClientState = (0x57F84C)
dwEntityList = (0x4A8574C)
dwLocalPlayer = (0xAAAAB4)
m_hActiveWeapon = (0x2EE8)
m_hMyWeapons = (0x2DE8)
m_iItemDefinitionIndex = (0x2F88)
m_iItemIDHigh = (0x2FA0)
m_nFallbackPaintKit = (0x3170)
m_nFallbackSeed = (0x3174)
m_nFallbackStatTrak = (0x317C)
m_flFallbackWear = (0x3178)
m_OriginalOwnerXuidLow = (0x3168)

pm = pymem.Pymem("csgo.exe")
client = pymem.process.module_from_name(pm.process_id, "client.dll").base_address
engine = pymem.process.module_from_name(pm.process_id, "engine.dll").base_address

def main():
    keyboard.add_hotkey('F6', lambda: change_skin())
    keyboard.add_hotkey('F7', lambda: force_full_update())
    keyboard.wait()

def force_full_update():
    engine_state = pm.read_int(engine + dwClientState)
    pm.write_int(engine_state + 0x174, -1)
    print("Update forced.")

def change_skin():
    paint = 51 # https://github.com/adamb70/CSGO-skin-ID-dumper/blob/master/item_index.txt
    local_player = pm.read_int(client + dwLocalPlayer)
    for i in range(0, 8): # Total possible inventory entities
        my_weapons = (pm.read_int(local_player + m_hMyWeapons + (i - 1) * 0x4) & 0xFFF)
        weapon_address = pm.read_int(client + dwEntityList + (my_weapons - 1) * 0x10)

        if weapon_address: # Not all inventory entities will exist
            weapon_id = pm.read_int(weapon_address + m_iItemDefinitionIndex)
            weapon_owner = pm.read_int(weapon_address + m_OriginalOwnerXuidLow)
            pm.write_int(weapon_address + m_iItemIDHigh, -1)
            pm.write_int(weapon_address + m_OriginalOwnerXuidLow, weapon_owner)
            pm.write_int(weapon_address + m_nFallbackStatTrak, -1)
            pm.write_int(weapon_address + m_iItemDefinitionIndex, weapon_id)
            pm.write_int(weapon_address + m_nFallbackPaintKit, paint)
            pm.write_int(weapon_address + m_nFallbackSeed, 661)
            pm.write_float(weapon_address + m_flFallbackWear, float(0.000000001))
            force_full_update()
            print("Set weapon skin values.")

if __name__ == '__main__':
    main()
using P3;
public class changeWeaponEvent : TrackerEvent
{
    public int ammo;
    public enum Weapon {KNIFE, PISTOL};

    public Weapon weapon;

    public changeWeaponEvent(int ammo_, Weapon weapon_) : base(EventType.CHANGE_WEAPON)
    {
        ammo = ammo_;
        weapon = weapon_;
    }
}

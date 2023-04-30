using P3;
public class playerAttackEvent : TrackerEvent
{
    public float posX, posY;
    public enum Weapon { KNIFE, PISTOL };

    public Weapon weapon;
    public playerAttackEvent(float posX_, float posY_, Weapon weapon_) : base(EventType.POS_PLAYER_ATTACK)
    {
        posX = posX_;
        posY = posY_;
        weapon = weapon_;
    }
}

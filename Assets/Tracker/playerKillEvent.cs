using P3;
public class playerKillEvent : TrackerEvent
{
    public float posX, posY;
    public enum Weapon { KNIFE, PISTOL };

    public Weapon weapon;
    public playerKillEvent(float posX_, float posY_, Weapon weapon_) : base(EventType.POS_PLAYER_KILL)
    {
        posX = posX_;
        posY = posY_;
        weapon = weapon_;
    }
}


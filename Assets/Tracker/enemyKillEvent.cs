using P3;
public class enemyKillEvent : TrackerEvent
{
    public float posX, posY;
    public enemyKillEvent(float posX_, float posY_) : base(EventType.POS_ENEMY_KILL)
    {
        posX = posX_;
        posY = posY_;
    }
}

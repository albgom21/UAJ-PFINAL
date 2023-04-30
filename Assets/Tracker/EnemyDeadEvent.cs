using P3;
public class EnemyDeadEvent : TrackerEvent
{
    public float posX, posY;
    public EnemyDeadEvent(float posX_, float posY_) : base(EventType.POS_ENEMY_DEAD)
    {
        posX = posX_;
        posY = posY_;
    }
}

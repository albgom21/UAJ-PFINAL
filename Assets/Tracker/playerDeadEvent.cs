using P3;
public class playerDeadEvent : TrackerEvent
{
    public float posX, posY;
    public enum TypeDead { LASER, ENEMY };

    public TypeDead dead;
    public playerDeadEvent(float posX_, float posY_, TypeDead dead_) : base(EventType.POS_PLAYER_DEAD)
    {
        posX = posX_;
        posY = posY_;
        dead = dead_;
    }
}


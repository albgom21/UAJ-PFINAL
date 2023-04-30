using P3;

public class playerInteractEvent : TrackerEvent
{
    public float posX, posY;

    public playerInteractEvent(float posX_, float posY_) : base(EventType.POS_PLAYER_INTERACT)
    {
        posX = posX_;
        posY = posY_;
    }
}
using P3;

public class exitRoomEvent : TrackerEvent
{
    public RoomID roomID;
    public exitRoomEvent(RoomID roomID_) : base(EventType.EXIT_ROOM)
    {
        roomID = roomID_;
    }
}
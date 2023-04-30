using P3;
public class enterRoomEvent : TrackerEvent
{
    public RoomID roomID;
    public enterRoomEvent(RoomID roomID_) : base(EventType.ENTER_ROOM)
    {
        roomID = roomID_;
    }
}
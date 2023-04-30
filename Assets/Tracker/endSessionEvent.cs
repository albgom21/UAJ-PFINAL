using P3;

public class endSessionEvent : TrackerEvent
{
    public string sessionID;
    public endSessionEvent() : base(EventType.END_SESSION)
    {
        sessionID = Tracker.Instance.GetSessionId();
    }

    public string getsessionID()
    {
        return sessionID;
    }
}
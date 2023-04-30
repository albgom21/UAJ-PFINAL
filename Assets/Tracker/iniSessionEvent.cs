namespace P3
{
    public class iniSessionEvent : TrackerEvent
    {
        public string sessionID;
        public iniSessionEvent() : base(EventType.INI_SESSION)
        {
            sessionID = Tracker.Instance.GetSessionId();
        }

        public string getsessionID()
        {
            return sessionID;
        }
    }
}
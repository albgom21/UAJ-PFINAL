using P3;
public class endLvlEvent : TrackerEvent
{
    public int lvlID;
    public endLvlEvent(int lvlid) : base(EventType.END_LVL)
    {
        lvlID = lvlid;
    }
}
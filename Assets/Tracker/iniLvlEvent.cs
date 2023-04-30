using P3;

public class iniLvlEvent : TrackerEvent
{
    public int lvlID;
    public iniLvlEvent(int lvlID_) : base(EventType.INI_LVL)
    {
        lvlID = lvlID_;
    }
}

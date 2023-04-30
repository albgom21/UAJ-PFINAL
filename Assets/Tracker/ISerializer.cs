namespace P3
{
    public abstract class ISerializer
    {
        public ISerializer() { }

        public abstract string Serialize(TrackerEvent te);
    }
}
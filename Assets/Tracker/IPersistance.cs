namespace P3
{
    public abstract class IPersistance
    {
        public IPersistance() { }

        public abstract void Send(TrackerEvent te);

        public abstract void Flush();
    }
}
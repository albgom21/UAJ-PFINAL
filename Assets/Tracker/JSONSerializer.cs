namespace P3
{
    public class JSONSerializer : ISerializer
    {
        public JSONSerializer() { }

        public override string Serialize(TrackerEvent te)
        {
            return te.ToJSON();
        }
    }
}

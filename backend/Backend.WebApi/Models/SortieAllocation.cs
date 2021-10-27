namespace Backend.WebApi.Models
{
    public class SortieAllocation
    {
        public Pilot Pilot { get; set; }

        public Jet Jet { get; set; }

        public Target Target { get; set; }

        public int MissileCount { get; set; }
    }
}

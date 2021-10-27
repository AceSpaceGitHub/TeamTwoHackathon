using System.Collections.Generic;

namespace Backend.WebApi.Models
{
    public class Carrier
    {
        public int InitialMissileCount { get; set; }

        public int MissileCount { get; set; }

        public List<Jet> Jets { get; set; }

        public List<Pilot> Pilots { get; set; }
    }
}

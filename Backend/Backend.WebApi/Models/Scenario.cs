using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace Backend.WebApi.Models
{
    public class Scenario
    {
        public Carrier Carrier1 { get; set; }

        public Carrier Carrier2 { get; set; }
    }

    public class Schedule
    {
        
    }

    public class Scheduler
    {
        Pilot GetPilot
    }

    public class Carrier
    {
        public int InitialMissileCount { get; set; }

        public int MissileCount { get; set; }

        public List<Jet> Jets { get; set; }

        public List<Pilot> Pilots { get; set; }
    }

    public class Jet
    {
        public string Id { get; set; }

        public bool IsDowned { get; set; }

        public int MyProperty { get; set; }
    }

    public class Pilot
    {
        public string Id { get; set; }
    }

    public class Sortie
    {
        public DateTime StartTime { get; set; }

        public DateTime EndTime { get; set; }

        public List<SortieAllocation> SortieAllocations { get; set; }
    }

    public class SortieAllocation
    {
        public Pilot Pilot { get; set; }

        public Jet Jet { get; set; }

        public Target Target { get; set; }

        public int MissileCount { get; set; }
    }

    public class Target
    {
        public string Id { get; set; }
    }

    public class AIResponse
    {

    }
}

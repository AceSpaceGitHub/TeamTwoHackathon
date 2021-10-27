using System;
using System.Collections.Generic;

namespace Backend.WebApi.Models
{
    public class Sortie
    {
        public DateTime StartTime { get; set; }

        public DateTime EndTime { get; set; }

        public List<SortieAllocation> SortieAllocations { get; set; }
    }
}

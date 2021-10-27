using System;
using System.Collections.Generic;

namespace Backend.WebApi.Models
{
    public class UISimulation
    {
        public int Missiles { get; set; }

        public int Jets { get; set; }

        public int Pilots { get; set; }

        public float SuccessRate { get; set; }

        public List<UIAction> Actions { get; set; }
    }

    public class UIAction
    {
        public DateTime StartTIme { get; set; }

        public DateTime EndTime { get; set; }
    }

    public class SortieAction : UIAction
    {
        public string Jet1 { get; set; }

        public string Jet2 { get; set; }

        public string Pilot1 { get; set; }

        public string Pilot2 { get; set; }

        public string Target1 { get; set; }

        public string Target2 { get; set; }

        public int Jet1Missiles { get; set; }

        public int Jet2Missiles { get; set; }
    }
}

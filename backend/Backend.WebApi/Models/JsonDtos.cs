namespace Backend.WebApi.Models
{

    public class Rootobject
    {
        public Result[] Results { get; set; }
    }

    public class Result
    {
        public Action[] Actions { get; set; }
        public float SuccessRate { get; set; }
    }

    public class Action
    {
        public int[] Actions { get; set; }
        public int[] Assets { get; set; }
        public int[] CurrentHits { get; set; }
        public int[] ExpectedHits { get; set; }
        public int Missiles { get; set; }
    }

    public class RequestDto
    {
        public int Missiles { get; set; }
        public int Pilots { get; set; }
        public int Jets { get; set; }
        public int[] ExpectedHits { get; set; }
    }

}

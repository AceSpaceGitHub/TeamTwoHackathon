using Backend.WebApi.Models;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Logging;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Http;
using System.Net.Http.Json;
using System.Threading.Tasks;

namespace Backend.WebApi.Controllers
{
    [ApiController]
    [Route("[controller]")]
    public class ScenarioController : ControllerBase
    {
        private static readonly string[] Summaries = new[]
        {
            "Freezing", "Bracing", "Chilly", "Cool", "Mild", "Warm", "Balmy", "Hot", "Sweltering", "Scorching"
        };

        private readonly ILogger<ScenarioController> _logger;

        public ScenarioController(ILogger<ScenarioController> logger)
        {
            _logger = logger;
        }

        [HttpGet]
        public async Task<UISimulation> Get()
        {

            using(var client = new HttpClient())
            {
                var response = await client.GetFromJsonAsync<Rootobject>(@"http://127.0.0.1:5001/api/v1/resources/scenario");

                var simulation = new UISimulation();

                var bestResult = response.Results.First();
                var lastState = bestResult.Actions.Last();

                simulation.SuccessRate = bestResult.SuccessRate;
                simulation.Missiles = lastState.Missiles;
                simulation.Jets = lastState.Assets[0];
                simulation.Pilots = lastState.Assets[1];
                simulation.Actions = new List<UIAction>();

                foreach (var sortie in bestResult.Actions)
                {
                    simulation.Actions.Add(new SortieAction()
                    {
                        Jet1 = "Jet 1",
                        Jet2 = "Jet 2",
                        Pilot1 = "Pilot 1",
                        Pilot2 = "Pilot 2",
                        Target1 = sortie.Actions[0].ToString(),
                        Target2 = sortie.Actions[1].ToString(),
                        Jet1Missiles = sortie.Actions[2],
                        Jet2Missiles = sortie.Actions[3],
                    });
                }

                return simulation;
            }
        }

        [HttpPost]
        public async Task<UISimulation> Post(RequestDto requestDto)
        {

            using (var client = new HttpClient())
            {
                var response = await client.GetFromJsonAsync<Rootobject>(@"http://127.0.0.1:5001/api/v1/resources/scenario");

                var simulation = new UISimulation();

                var bestResult = response.Results.First();
                var lastState = bestResult.Actions.Last();

                simulation.SuccessRate = bestResult.SuccessRate;
                simulation.Missiles = lastState.Missiles;
                simulation.Jets = lastState.Assets[0];
                simulation.Pilots = lastState.Assets[1];
                simulation.Actions = new List<UIAction>();

                foreach (var sortie in bestResult.Actions)
                {
                    simulation.Actions.Add(new SortieAction()
                    {
                        Jet1 = "Jet 1",
                        Jet2 = "Jet 2",
                        Pilot1 = "Pilot 1",
                        Pilot2 = "Pilot 2",
                        Target1 = sortie.Actions[0].ToString(),
                        Target2 = sortie.Actions[1].ToString(),
                        Jet1Missiles = sortie.Actions[2],
                        Jet2Missiles = sortie.Actions[3],
                    });
                }

                return simulation;
            }
        }
    }
}

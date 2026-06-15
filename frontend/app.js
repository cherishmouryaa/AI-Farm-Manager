document.addEventListener('DOMContentLoaded', () => {
    const farmForm = document.getElementById('farmForm');
    const submitBtn = document.getElementById('submitBtn');
    const btnSpinner = submitBtn.querySelector('.btn-spinner');
    const btnText = submitBtn.querySelector('.btn-text');
    
    const emptyState = document.getElementById('emptyState');
    const planOutput = document.getElementById('planOutput');
    
    // Output UI targets
    const weatherTemp = document.getElementById('weatherTemp');
    const weatherHumidity = document.getElementById('weatherHumidity');
    const weatherRainStatus = document.getElementById('weatherRainStatus');
    const weatherOutlook = document.getElementById('weatherOutlook');
    
    const cropTitle = document.getElementById('cropTitle');
    const recList = document.getElementById('recList');
    
    const cardAcreage = document.getElementById('cardAcreage');
    const finCost = document.getElementById('finCost');
    const finRevenue = document.getElementById('finRevenue');
    const finProfit = document.getElementById('finProfit');
    
    const taskDay1 = document.getElementById('taskDay1');
    const taskDay2 = document.getElementById('taskDay2');
    const taskDay3 = document.getElementById('taskDay3');
    const taskDay4 = document.getElementById('taskDay4');
    const taskDay5 = document.getElementById('taskDay5');
    const taskDay6 = document.getElementById('taskDay6');
    const taskDay7 = document.getElementById('taskDay7');

    farmForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // Disable form during request
        submitBtn.disabled = true;
        btnSpinner.classList.remove('hidden');
        btnText.textContent = "Analyzing Land System...";
        
        const formData = {
            location: document.getElementById('location').value,
            crop: document.getElementById('crop').value,
            farm_size: parseFloat(document.getElementById('farmSize').value),
            soil_type: document.getElementById('soilType').value,
            water_source: document.getElementById('waterSource').value
        };

        try {
            console.log("Sending plan query to FastAPI AI Farm Manager:", formData);
            
            // Assume backend exists at: POST /farm-plan
            const response = await fetch('/farm-plan', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            renderPlanOutput(data, formData);

        } catch (error) {
            console.warn("FastAPI backend /farm-plan unreachable. Launching client-side fallback demo handler.", error);
            // Simulate API logic locally with precise values based on user input
            setTimeout(() => {
                const simulatedData = generateOfflineFarmPlan(formData);
                renderPlanOutput(simulatedData, formData);
            }, 800); // realistic network delay
        } finally {
            submitBtn.disabled = false;
            btnSpinner.classList.add('hidden');
            btnText.textContent = "Generate Farm Plan";
        }
    });

    function renderPlanOutput(data, inputs) {
        // Hide empty state and show results cards
        emptyState.classList.add('hidden');
        planOutput.classList.remove('hidden');

        // Update Weather Section
        weatherTemp.textContent = data.weather?.temp || "34°C";
        weatherHumidity.textContent = data.weather?.humidity || "62%";
        weatherRainStatus.textContent = data.weather?.rain_forecast || "Moderate chance of rain";
        weatherOutlook.textContent = data.weather?.outlook || `Typical ${inputs.location} district microclimate. Plan operations around morning humidity drops.`;

        // Update Crop Recommendations
        cropTitle.textContent = inputs.crop;
        recList.innerHTML = '';
        const recs = data.recommendations || [
            "Apply gypsum during pegging stage.",
            "Monitor for leaf miner and red hairy caterpillar.",
            "Maintain proper irrigation schedule."
        ];
        recs.forEach(rec => {
            const li = document.createElement('li');
            li.textContent = rec;
            recList.appendChild(li);
        });

        // Update Profit Card (with indian rupees formatting)
        cardAcreage.textContent = `${inputs.farm_size} Acres`;
        
        const formatter = new Intl.NumberFormat('en-IN', {
            style: 'currency',
            currency: 'INR',
            maximumFractionDigits: 0
        });

        finCost.textContent = formatter.format(data.budget?.estimated_cost || 45000);
        finRevenue.textContent = formatter.format(data.budget?.expected_revenue || 75000);
        finProfit.textContent = formatter.format(data.budget?.expected_profit || 30000);

        // Update Weekly tasks
        const fallbackTasks = [
            "Soil moisture check and irrigation inspection",
            "Apply gypsum and micronutrients",
            "Weed removal and field monitoring",
            "Pest inspection and preventive spray",
            "Irrigation management",
            "Review crop growth and nutrient status",
            "Prepare next week's farm activities"
        ];
        const weeklyTasks = data.weekly_planner || fallbackTasks;
        
        taskDay1.textContent = weeklyTasks[0] || "";
        taskDay2.textContent = weeklyTasks[1] || "";
        taskDay3.textContent = weeklyTasks[2] || "";
        taskDay4.textContent = weeklyTasks[3] || "";
        taskDay5.textContent = weeklyTasks[4] || "";
        taskDay6.textContent = weeklyTasks[5] || "";
        taskDay7.textContent = weeklyTasks[6] || "";

        // Scroll results into view smoothly
        planOutput.scrollIntoView({ behavior: 'smooth' });
    }

    // Function to generate extremely detailed simulations matching AP farming terminology & requirements
    function generateOfflineFarmPlan(inputs) {
        const size = inputs.farm_size;
        
        // Default weather details for the regions
        let temp = "34°C";
        let humidity = "62%";
        let rain_forecast = "Moderate chance of rain";
        let outlook = "";

        if (inputs.location === "Naidupeta" || inputs.location === "Nellore") {
            temp = "35°C";
            humidity = "64%";
            rain_forecast = "Moderate coastal clouds, scattered showers";
            outlook = `Coastal breeze from Bay of Bengal brings moisture to ${inputs.location} lands. Watch out for humidity spikes.`;
        } else if (inputs.location === "Tirupati") {
            temp = "34°C";
            humidity = "62%";
            rain_forecast = "Light brief showers, mostly sunny";
            outlook = `Sub-tropical dry spell over Tirupati ranges. Optimal conditions for pegging activities if hydration matches soil rates.`;
        } else {
            temp = "33°C";
            humidity = "60%";
            rain_forecast = "Dry solar conditions, moderate clouds";
            outlook = `Mild afternoon wind from nearby irrigation tanks expected. Maintain stable furrow moistures.`;
        }

        // Recommendations based on Crop
        let recs = [];
        let costPerAcre = 9000;
        let revPerAcre = 15000;
        let weekly = [];

        switch(inputs.crop) {
            case "Groundnut":
                recs = [
                    "Apply gypsum during pegging stage (at 40-45 days) to enhance pod filling.",
                    "Monitor fields daily for leaf miner and red hairy caterpillar.",
                    "Maintain proper irrigation schedule especially during flowering and pegging."
                ];
                costPerAcre = 9000;
                revPerAcre = 15000;
                weekly = [
                    "Soil moisture check and irrigation inspection",
                    "Apply gypsum and micronutrients",
                    "Weed removal and field monitoring",
                    "Pest inspection and preventive spray",
                    "Irrigation management",
                    "Review crop growth and nutrient status",
                    "Prepare next week's farm activities"
                ];
                break;
            case "Paddy":
                recs = [
                    "Maintain shallow standing water layer of 2-5 cm in wetland fields.",
                    "Perform split application of nitrogen (Urea) at tillering and panicle initiation.",
                    "Look out for Yellow Stem Borer moths and blast symptoms; spray neem compound."
                ];
                costPerAcre = 14000;
                revPerAcre = 24000;
                weekly = [
                    "Clear standing weeds surrounding bund walls",
                    "Top-dress paddies with nitrogen fertilizer",
                    "Release Azolla bio-fertilizer over puddle beds",
                    "Inspect under leaves for blast disease or brown planthoppers",
                    "Manage wetland water intake levels",
                    "Assess crop tillers and average growth stature",
                    "Calculate next week's organic fertilizer procurement"
                ];
                break;
            case "Sugarcane":
                recs = [
                    "Erect soil support mounts (earthing-up) at 3-4 months to avoid lodging.",
                    "Apply nitrogenous fertilizer alongside potassium in trenches.",
                    "Monitor shoot borers and ensure trash mulching in early crop stages."
                ];
                costPerAcre = 18000;
                revPerAcre = 32000;
                weekly = [
                    "Irrigate sugar furrows and check trench moisture",
                    "Apply potassium dose to enhance juice content",
                    "Remove weeds and clean loose soil under canopies",
                    "Examine top inner shoots for early shoot borer",
                    "Deep-irrigation cycle management",
                    "Perform hand trimming of yellowing bottom leaves",
                    "Map out next week's labor schedule for earthing-up"
                ];
                break;
            case "Mango":
                recs = [
                    "Prune overcrowded and dead inner branches after harvest to allow high solar penetration.",
                    "Observe for web worm or hopper spikes during flowering cycles.",
                    "Provide basin irrigation under major canopy drop lines."
                ];
                costPerAcre = 7000;
                revPerAcre = 18000;
                weekly = [
                    "Inspect mango tree basin rings for uniform water intake",
                    "Incorporate compost and minor phosphorus into the basins",
                    "Clear weeds in between major crop lines",
                    "Spray preventive trace elements for hopper controls",
                    "Calibrate mini basin watering feeds",
                    "Examine leaves and twigs for powdery mildew signs",
                    "Detail plan for canopy growth pruning"
                ];
                break;
            case "Lemon":
                recs = [
                    "Apply balanced nitrogen, phosphorus, and potassium along with zinc micro-feeds.",
                    "Vigilantly track leaf-miner tunnels on tender fresh foliage.",
                    "Irrigate thoroughly during fruit development stages to prevent small yield shapes."
                ];
                costPerAcre = 8000;
                revPerAcre = 16000;
                weekly = [
                    "Confirm drip emitter discharge rates under citrus trunks",
                    "Inject water-soluble calcium nitrate into drip lines",
                    "Prune basal suckers and root shoots below graft points",
                    "Inspect lemons for scale insects and direct leaf miner tracks",
                    "Drip cycle scheduling",
                    "Review general citrus foliage color index",
                    "Formulate micro-nutrient foliar spray list for Sunday"
                ];
                break;
        }

        // Calculate size based values
        const finalCost = costPerAcre * size;
        const finalRev = revPerAcre * size;
        const finalProfit = finalRev - finalCost;

        return {
            weather: {
                temp,
                humidity,
                rain_forecast,
                outlook
            },
            recommendations: recs,
            budget: {
                estimated_cost: finalCost,
                expected_revenue: finalRev,
                expected_profit: finalProfit
            },
            weekly_planner: weekly
        };
    }
});

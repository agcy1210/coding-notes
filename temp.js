$db.population.aggregate([
    { $match: { "Year": 2014 } },

    {
        $project: {
            'County Name': 1,
            Female: {
                $cond: [ { $eq: ["$Gender", "Female"]}, "$Population", 0]
            },
            Male: {
                $cond: [{ $eq: ["$Gender", "Male"] }, "$Population", 0]
            },
        }
    },
    {
        $group: {
            _id: "County Name",
            Female: { $sum: "$Female" },
            Male: { $sum: "$Male" }
        }
    },
    { $sort: { _id: 1 } }]
) 
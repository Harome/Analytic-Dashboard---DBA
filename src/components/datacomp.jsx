import React, { useState, useEffect, useCallback } from 'react';
import './datacomp.css';
import Plot from 'react-plotly.js';

const DataComp = () => {
    const [category, setCategory] = useState("");
    const [genderComparison, setGenderComparison] = useState(null);
    const [region, setRegion] = useState("All Regions");
    const [regions, setRegions] = useState([]);
    const [loading, setLoading] = useState(false); // Add a loading state
    const [error, setError] = useState(null);     // Add an error state

    const handleCategoryChange = (e) => setCategory(e.target.value);
    const handleRegionChange = (e) => setRegion(e.target.value);

    // Fetch regions on component mount
    useEffect(() => {
        const fetchRegions = async () => {
            setLoading(true); // Start loading
            setError(null);    // Clear any previous errors
            try {
                const response = await fetch("http://127.0.0.1:8050/api/regions");
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                const data = await response.json();
                setRegions(data);
            } catch (error) {
                console.error("Error fetching regions:", error);
                setError(error.message); // Set the error message
            } finally {
                setLoading(false); // Stop loading regardless of success/failure
            }
        };

        fetchRegions();
    }, []);

    const fetchGenderComparison = useCallback(async () => {
        if (category !== "gender") return; // Only fetch if category is "gender"

        setLoading(true);
        setError(null);
        try {
            const response = await fetch(`http://127.0.0.1:8050/api/gender-comparison?region=${region}`);
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            const data = await response.json();
            console.log("Fetched gender comparison data:", data); // Debugging
            setGenderComparison(data);
        } catch (error) {
            console.error("Error fetching gender comparison:", error);
            setError(error.message);
            setGenderComparison(null); // Clear data on error
        } finally {
            setLoading(false);
        }
    }, [region, category]); // Add category as a dependency

    useEffect(() => {
        fetchGenderComparison(); // Fetch when region or category changes
    }, [region, fetchGenderComparison, category]);

    return (
        <div className="datacomp-container">
            <header className="datacomp-header">
                <h1>Data Comparison</h1>
            </header>

            <div className="outer-container">
                <div className="dropdowns-row">
                    <select className="dropdown left-dropdown" value={category} onChange={handleCategoryChange}>
                        <option value="">Select Category</option>
                        <option value="gender">Gender</option>
                        <option value="grade-level">Grade Level</option>
                        <option value="grade-division">Grade Division</option>
                        <option value="sector">Sector</option>
                        <option value="school-type">School Type</option>
                    </select>
                    {category === "gender" && (
                        <select className="dropdown right-dropdown" value={region} onChange={handleRegionChange}>
                            <option value="All Regions">All Regions</option>
                            {regions.map(reg => (
                                <option key={reg} value={reg}>{reg}</option>
                            ))}
                        </select>
                    )}
                </div>

                <div className="datacomp-wrapper">
                    <div className="container-with-sticker">
                        <div className="container-icon">1</div>
                        <div className="left-container">
                            {loading && <div>Loading...</div>}
                            {error && <div style={{ color: 'red' }}>Error: {error}</div>}
                            {category === "gender" && genderComparison && genderComparison.data && genderComparison.layout && (
                                <Plot
                                    data={genderComparison.data}
                                    layout={genderComparison.layout}
                                    style={{ width: '100%', height: '400px' }}
                                />
                            )}
                            {category === "gender" && !genderComparison && !loading && !error && <div>No data available.</div>}
                        </div>
                    </div>

                    <div className="container-with-sticker">
                        <div className="container-icon">2</div>
                        <div className="right-container">
                            {/* Right content */}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default DataComp;
import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

const ApplicationForm = () => {
    // Form state
    const [formData, setFormData] = useState({
        first_name: "",
        last_name: "",
        email: "",
        phone: "",
        address_1: "",
        address_2: "",
        city: "",
        state: "",
        zip_code: "",
        ssn: "",
        requested_amount: "",
    });

    const navigate = useNavigate();
    const [error, setError] = useState(null);

    // Handle input changes on the form
    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value,
        });
    };

    // Handle form submission
    const handleSubmit = async (e) => {
        e.preventDefault(); // Prevent page reload on submit
        setError(null);

        const payload = {
            borrower: {
                first_name: formData.first_name,
                last_name: formData.last_name,
                email: formData.email,
                phone: formData.phone,
                address_1: formData.address_1,
                address_2: formData.address_2,
                city: formData.city,
                state: formData.state,
                zip_code: formData.zip_code,
                ssn: formData.ssn,
            },
            requested_amount: parseFloat(formData.requested_amount),
        };

        // Submit application to backend (Currently hardcoded URL of localhost)
        try {
            const res = await axios.post(
                "http://localhost:5000/api/applications",
                payload
            ); // Adjust URL as needed // Hardcoded for now
            navigate("/result", { state: { application: res.data } });
        } catch (err) {
            setError(
                "An error occurred while submitting the application. Plese try again."
            );
        }
    };
    // Render the form
    return (
        <div className="p-6 max-w-lg mx-auto">
            <h2 className="text-2xl font-semibold mb-4">Loan Application</h2>

            {error && <p className="text-red-500">{error}</p>}

            <form onSubmit={handleSubmit} className="space-y-3">
                <input
                    name="first_name"
                    placeholder="First Name"
                    onChange={handleChange}
                    required
                    className="w-full p-2 border rounded"
                />
                <input
                    name="last_name"
                    placeholder="Last Name"
                    onChange={handleChange}
                    required
                    className="w-full p-2 border rounded"
                />
                <input
                    name="email"
                    placeholder="Email"
                    type="email"
                    onChange={handleChange}
                    required
                    className="w-full p-2 border rounded"
                />
                <input
                    name="phone"
                    placeholder="Phone: ###-###-####"
                    onChange={handleChange}
                    className="w-full p-2 border rounded"
                />
                <input
                    name="address_1"
                    placeholder="Address 1"
                    onChange={handleChange}
                    required
                    className="w-full p-2 border rounded"
                />
                <input
                    name="address_2"
                    placeholder="Address 2"
                    onChange={handleChange}
                    className="w-full p-2 border rounded"
                />
                <input
                    name="city"
                    placeholder="City"
                    onChange={handleChange}
                    required
                    className="w-full p-2 border rounded"
                />
                <input
                    name="state"
                    placeholder="State"
                    onChange={handleChange}
                    required
                    className="w-full p-2 border rounded"
                />
                <input
                    name="zip_code"
                    placeholder="Zip Code"
                    onChange={handleChange}
                    required
                    className="w-full p-2 border rounded"
                />
                <input
                    name="ssn"
                    placeholder="SSN: ###-##-####"
                    onChange={handleChange}
                    required
                    className="w-full p-2 border rounded"
                />
                <div className="relative">
                    <span className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-500">
                        $
                    </span>
                    <input
                        name="requested_amount"
                        placeholder="Requested Amount"
                        type="number"
                        onChange={handleChange}
                        required
                        className="w-full pl-7 p-2 border rounded" // pl-7 leaves space for $
                    />
                </div>
                <button
                    type="submit"
                    className="w-full bg-blue-600 text-white p-2 rounded hover:bg-blue-700"
                >
                    Submit
                </button>
            </form>
        </div>
    );
};

export default ApplicationForm;

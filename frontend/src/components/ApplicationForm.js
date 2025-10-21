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
    const [fieldErrors, setFieldErrors] = useState({});

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
        setFieldErrors({});

        // Prepare payload
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
                `${process.env.REACT_APP_URL}/api/applications`,
                payload
            ); // Adjust URL as needed // Hardcoded for now
            navigate("/result", { state: { application: res.data } });
        } catch (err) {
            if (err.response?.data?.errors?.borrower) {
                setFieldErrors(err.response.data.errors.borrower);
            } else {
                setError(
                    err.response?.data?.message || err.response?.data?.errors ||
                    "An error occurred while submitting the application. Please try again."
                );
            }
        }
    };
    // Render the form
    return (
        <div className="p-6 w-full max-w-lg sm:max-w-md mx-auto">
            <h2 className="text-2xl font-semibold mb-4">Personal Loan Application</h2>

            {error && <p className="text-red-500">{error}</p>}

            <form onSubmit={handleSubmit} className="space-y-3">
                <div>
                    <label
                        htmlFor="first_name"
                        className="block font-medium mb-1"
                    >
                        First Name <span style={{ color: 'red' }}>*</span>
                    </label>
                    <input
                        id="first_name"
                        name="first_name"
                        onChange={handleChange}
                        required
                        className="w-full p-2 border rounded"
                        placeholder="John"
                    />
                </div>

                <div>
                    <label
                        htmlFor="last_name"
                        className="block font-medium mb-1"
                    >
                        Last Name <span style={{ color: 'red' }}>*</span>
                    </label>
                    <input
                        id="last_name"
                        name="last_name"
                        onChange={handleChange}
                        required
                        className="w-full p-2 border rounded"
                        placeholder="Doe"
                    />
                </div>

                <div>
                    <label htmlFor="email" className="block font-medium mb-1">
                        Email <span style={{ color: 'red' }}>*</span>
                    </label>
                    <input
                        id="email"
                        name="email"
                        type="email"
                        onChange={handleChange}
                        required
                        className="w-full p-2 border rounded"
                        placeholder="email@email.com"
                    />
                    {fieldErrors.phone && (
                        <p className="text-red-500 text-sm">{fieldErrors.phone[0]}</p>
                    )}
                </div>

                <div>
                    <label htmlFor="phone" className="block font-medium mb-1">
                        Phone <span style={{ color: 'red' }}>*</span>
                    </label>
                    <input
                        id="phone"
                        name="phone"
                        onChange={handleChange}
                        required
                        className="w-full p-2 border rounded"
                        placeholder="555-555-5555"
                    />
                    {fieldErrors.phone && (
                        <p className="text-red-500 text-sm">{fieldErrors.phone[0]}</p>
                    )}
                </div>

                <div>
                    <label
                        htmlFor="address_1"
                        className="block font-medium mb-1"
                    >
                        Address 1 <span style={{ color: 'red' }}>*</span>
                    </label>
                    <input
                        id="address_1"
                        name="address_1"
                        onChange={handleChange}
                        required
                        className="w-full p-2 border rounded"
                        placeholder="123 Main St"
                    />
                </div>

                <div>
                    <label
                        htmlFor="address_2"
                        className="block font-medium mb-1"
                    >
                        Address 2 <span style={{ color: 'red' }}>*</span>
                    </label>
                    <input
                        id="address_2"
                        name="address_2"
                        onChange={handleChange}
                        className="w-full p-2 border rounded"
                        placeholder="Apt 4B"
                    />
                </div>

                <div>
                    <label htmlFor="city" className="block font-medium mb-1">
                        City <span style={{ color: 'red' }}>*</span>
                    </label>
                    <input
                        id="city"
                        name="city"
                        onChange={handleChange}
                        required
                        className="w-full p-2 border rounded"
                        placeholder="Springfield"
                    />
                </div>

                <div>
                    <label htmlFor="state" className="block font-medium mb-1">
                        State <span style={{ color: 'red' }}>*</span>
                    </label>
                    <input
                        id="state"
                        name="state"
                        onChange={handleChange}
                        required
                        className="w-full p-2 border rounded"
                        placeholder="IL"
                    />
                </div>

                <div>
                    <label
                        htmlFor="zip_code"
                        className="block font-medium mb-1"
                    >
                        Zip Code <span style={{ color: 'red' }}>*</span>
                    </label>
                    <input
                        id="zip_code"
                        name="zip_code"
                        onChange={handleChange}
                        required
                        className="w-full p-2 border rounded"
                        placeholder="62704"
                    />
                </div>

                <div>
                    <label htmlFor="ssn" className="block font-medium mb-1">
                        SSN <span style={{ color: 'red' }}>*</span>
                    </label>
                    <input
                        id="ssn"
                        name="ssn"
                        onChange={handleChange}
                        required
                        className="w-full p-2 border rounded"
                        placeholder="123-45-6789"
                    />
                    {fieldErrors.ssn && (
                        <p className="text-red-500 text-sm">
                            {fieldErrors.ssn[0]}
                        </p>
                    )}
                </div>
                <div className="relative">
                    <label
                        htmlFor="requested_amount"
                        className="block font-medium mb-1"
                    >
                        Requested Amount <span style={{ color: 'red' }}>*</span>
                    </label>
                    <span className="absolute left-2 top-1/2 transform -translate-y-1/5 text-gray-500">
                        $
                    </span>
                    <input
                        name="requested_amount"
                        placeholder="0.00"
                        type="number"
                        onChange={handleChange}
                        required
                        className="w-full pl-6 p-2 border rounded" // pl-7 leaves space for $
                    />
                </div>
                <button
                    type="submit"
                    className="w-full sm:w-full bg-blue-600 text-white p-2 rounded hover:bg-blue-700"
                >
                    Submit
                </button>
            </form>
        </div>
    );
};

export default ApplicationForm;

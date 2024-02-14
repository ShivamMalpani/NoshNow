import React, { useState, useEffect } from 'react';
import './Menu.css';
import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button';

const Menu = () => {
    
    useEffect(() => {
        fetch('https://cd80-14-139-54-194.ngrok-free.app/api/catalogue/students/item_list/1', {
            headers: {
                'ngrok-skip-browser-warning': 'true'
            }
        })
        .then(response => {
            console.log(response);
            return response.json();
        })
        .then(data => {
            console.log(data);
            setItems(data);
        })
        .catch(error => console.error('Error fetching items:', error));
    }, []);
    // Define fetchItemList function to fetch the list of items from the server
    const fetchItemList = () => {
        fetch('https://cd80-14-139-54-194.ngrok-free.app/api/catalogue/students/item_list/1')
            .then(response => response.json())
            .then(data => {
                console.log(data);
                setItems(data);
            })
            .catch(error => console.error('Error fetching items:', error));
    };




    // State to manage form fields for adding an item
    const [name, setName] = useState('');
    const [cost, setCost] = useState('');
    const [image, setImage] = useState(''); // Changed from imageUrl to image
    const [description, setDescription] = useState('');
    const [instantItem, setInstantItem] = useState(false);
    const [available, setAvailable] = useState(false);
    const [quantity, setQuantity] = useState('');

    // State to manage form fields for updating an item
    const [updateName, setUpdateName] = useState('');
    const [updateCost, setUpdateCost] = useState('');
    const [updateImage, setUpdateImage] = useState(''); // Changed from updateImageUrl to updateImage
    const [updateDescription, setUpdateDescription] = useState('');
    const [updateInstantItem, setUpdateInstantItem] = useState(false);
    const [updateAvailable, setUpdateAvailable] = useState(false);
    const [updateQuantity, setUpdateQuantity] = useState('');
    const [itemIdToUpdate, setItemIdToUpdate] = useState('');
    // State to manage visibility of Add Item and Update Item forms
    const [showAddForm, setShowAddForm] = useState(false);
    const [showUpdateForm, setShowUpdateForm] = useState(false);

    // State to manage existing items
    const [items, setItems] = useState([]);

    // Function to handle form submission when adding an item
    const handleAddItem = (e) => {
        e.preventDefault();
        const newItemData = {
 // Assuming userID is always 1 for now
            userID: 1,
            name,
            cost,
            image,
            description,
            instant_item: instantItem,
            available,
            quantity
        };
    
        fetch('https://cd80-14-139-54-194.ngrok-free.app/api/catalogue/restaurant/add_item', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(newItemData)
        })
        .then(response => response.json())
        .then(data => {
            console.log('Item added successfully:', data);
            // Assuming you want to update the list of items after adding a new item
            fetchItemList();
            resetAddForm(); // Reset form fields after successful addition
        })
        .catch(error => console.error('Error adding item:', error));
        window.location.reload();

    };
    

    // Function to handle form submission when updating an item
    const handleUpdateItem = (e) => {
        e.preventDefault();
        // console.log(e);
        const updatedItemData = {
            userID: 1,
            itemID: itemIdToUpdate, // Assuming you have a variable itemIdToUpdate that holds the ID of the item to update
            name: updateName,
            cost: updateCost,
            image : updateImage,
            description: updateDescription,
            instant_item: updateInstantItem,
            available: updateAvailable,
            quantity: updateQuantity
        };
        console.log('Updating Item:', updatedItemData);
        window.location.reload();
        fetch('https://cd80-14-139-54-194.ngrok-free.app/api/catalogue/restaurant/update_item', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(updatedItemData)
        })
        .then(response => response.json())
        .then(data => {
            console.log('Item updated successfully:', data);
            // Assuming you want to update the list of items after updating an item
            fetchItemList();
            resetUpdateForm(); // Reset form fields after successful update
        })
        .catch(error => console.error('Error updating item:', error));
    };
    
    const handleDeleteItem = (itemId) => {
        const deleteItemData = {
            userID: 1, // Assuming userID is always 1 for now
            itemID: itemId
        };
        console.log(deleteItemData)
        fetch('https://cd80-14-139-54-194.ngrok-free.app/api/catalogue/restaurant/delete_item', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(deleteItemData)
        })
        .then(response => response.json())
        .then(data => {
            console.log('Item deleted successfully:', data);
        })
        .catch(error => console.error('Error deleting item:', error));
        window.location.reload();
    };
    // Function to reset Add Item form fields
    const resetAddForm = () => {
        setName('');
        setCost('');
        setImage('');
        setDescription('');
        setInstantItem(false);
        setAvailable(true);
        setQuantity('');
    };

    // Function to reset Update Item form fields
    const resetUpdateForm = () => {
        setUpdateName('');
        setUpdateCost('');
        setUpdateImage('');
        setUpdateDescription('');
        setUpdateInstantItem(false);
        setUpdateAvailable(true);
        setUpdateQuantity('');
        setItemIdToUpdate('');
    };

    // Function to handle click on an item image to show update form
    const handleItemClick = (item) => {
        setItemIdToUpdate(item.id); 
        setUpdateName(item.name);
        setUpdateCost(item.cost);
        setUpdateImage(item.image); // Changed from item.imageUrl to item.image
        setUpdateDescription(item.description);
        setUpdateInstantItem(item.instantItem);
        setUpdateAvailable(item.available);
        setUpdateQuantity(item.quantity);
        setShowUpdateForm(true);
    };

    return (
        <>
            {/* Button to toggle Add Item form visibility */}
            <button className="add-item-button add-button" onClick={() => setShowAddForm(!showAddForm)}>
                {showAddForm ? 'Hide Add Form' : 'Add Item'}
            </button>
            {showAddForm && (
                <form className="add-item-form" onSubmit={handleAddItem}>
                    {/* Form fields for adding an item */}
                    {/* Use onChange handlers to update state when user inputs */}
                    <input type="text" placeholder="Name" value={name} onChange={(e) => setName(e.target.value)} />
                    <input type="number" placeholder="Cost" value={cost} onChange={(e) => setCost(e.target.value)} />
                    <input type="text" placeholder="Image URL" value={image} onChange={(e) => setImage(e.target.value)} />
                    <input type="text" placeholder="Description" value={description} onChange={(e) => setDescription(e.target.value)} />
                    <input type="checkbox" checked={instantItem} onChange={(e) => setInstantItem(e.target.checked)} />
                    <label>Instant Item</label>
                    <input type="checkbox" checked={available} onChange={(e) => setAvailable(e.target.checked)} />
                    <label>Available</label>
                    <input type="number" placeholder="Quantity" value={quantity} onChange={(e) => setQuantity(e.target.value)} />
                    <button type="submit">Add Item</button>
                </form>
            )}
            <div className="menu-container">
                <div className="existing-items menu-items-container">
                {items.map(item => (
                    <Card key={item.id} className="item-card">
                    <Card.Img className='item-image' variant="top" src={item.image} alt={item.name} />
                    <Card.Body>
                        <Card.Title className='item-name'>{item.name}</Card.Title>
                        <Card.Text>
                            <p className='cost'>Cost: {item.cost}</p>
                            <p className='quantity'>Quantity: {item.quantity}</p>
                        </Card.Text>
                        <Button className='button-baby' variant="primary" onClick={() => handleItemClick(item)}>Update Item</Button>
                        <Button className='button-baby' variant="danger" onClick={() => handleDeleteItem(item.id)}>Delete Item</Button>
                    </Card.Body>
                </Card>
                ))}
                </div>
            </div>
                            {/* Update Item Form */}
                            {showUpdateForm && (
                    <form className="update-item-form add-item-form" onSubmit={handleUpdateItem}>
                        {/* Form fields for updating an item */}
                        {/* Use onChange handlers to update state when user inputs */}
                        <input type="text" placeholder="Name" value={updateName} onChange={(e) => setUpdateName(e.target.value)} />
                        <input type="number" placeholder="Id" value={itemIdToUpdate} onChange={(e) => setItemIdToUpdate(e.target.value)} />
                        <input type="number" placeholder="Cost" value={updateCost} onChange={(e) => setUpdateCost(e.target.value)} />
                        <input type="text" placeholder="Image URL" value={updateImage} onChange={(e) => setUpdateImage(e.target.value)} />
                        <input type="text" placeholder="Description" value={updateDescription} onChange={(e) => setUpdateDescription(e.target.value)} />
                        <input type="checkbox" checked={updateInstantItem} onChange={(e) => setUpdateInstantItem(e.target.checked)} />
                        <label>Instant Item</label>
                        <input type="checkbox"  checked={updateAvailable} onChange={(e) => setUpdateAvailable(e.target.checked)} />
                        <label>Available</label>
                        <input type="number" placeholder="Quantity" value={updateQuantity} onChange={(e) => setUpdateQuantity(e.target.value)} />
                        <button type="submit">Update Item</button>
                    </form>
                )}
        </>
    );
};

export default Menu;

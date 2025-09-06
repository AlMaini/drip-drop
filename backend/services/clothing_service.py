import io
import json
import time
import base64
import os
import asyncio
from typing import List
from fastapi import UploadFile
from PIL import Image
from google import genai
from google.genai import types

from .gemini_client import get_gemini_client, editing_model, analysis_model
from .image_processing import process_uploaded_image, image_to_base64
import processing.utility.image_utils as image_utils

async def extract_single_clothing_item(image: UploadFile) -> dict:
    """Extract clothing item from photo and create professional product image"""
    client = get_gemini_client()
    
    # Process uploaded image
    processed_image = process_uploaded_image(image)
    
    # Create the extraction prompt
    prompt = "Take the clothing item in this photo and make a full view image of the item with a white background as a professionally shot image for a clothing item on an online store. Do not change any details from the clothes. Be as accurate as possible."
    
    # Prepare content for Gemini
    contents = [prompt, processed_image]
    
    # Generate the professional product image
    response = client.models.generate_content(
        model=editing_model,
        contents=contents
    )
    
    # Process response - check for both generated image and text description
    generated_image_base64 = None
    description_text = None
    
    for part in response.candidates[0].content.parts:
        if part.text is not None:
            description_text = part.text
        elif part.inline_data is not None:
            image_data = Image.open(io.BytesIO(part.inline_data.data))
            padded_image = image_utils.pad_image_to_square(image_data)
            generated_image_base64 = image_to_base64(padded_image)

    return {
        "generated_image_base64": generated_image_base64,
        "description": description_text if description_text else "Professional clothing product image generated"
    }

async def analyze_clothing_quality(image: UploadFile) -> dict:
    """Check if an image is a professional studio quality photo of a single clothing item"""
    processed_image = process_uploaded_image(image)
    return check_professional_clothing_image(processed_image)

def check_professional_clothing_image(image: Image.Image) -> dict:
    """
    Check if an image is a professional studio quality photo of a single clothing item
    
    Args:
        image: PIL Image object to analyze
        
    Returns:
        dict: Analysis results containing is_professional, is_single_item, item_type, and confidence
    """
    client = get_gemini_client()
    
    try:
        # Create analysis prompt
        prompt = """
        Analyze this image and determine if it meets the following criteria:
        1. Is it a professional studio quality photograph?
        2. Does it contain exactly one clothing item?
        3. Is the background clean/plain (preferably white or neutral)?
        4. Is the lighting professional and even?
        5. Is the clothing item the main focus and clearly visible?
        
        Please respond in the following JSON format:
        {
            "is_professional": true/false,
            "is_single_item": true/false,
            "item_type": "shirt/pants/dress/shoes/etc or null if not clothing",
            "background_quality": "excellent/good/poor",
            "lighting_quality": "excellent/good/poor",
            "overall_confidence": 0.0-1.0,
            "issues": ["list of any issues found"],
            "reasoning": "brief explanation of the assessment"
        }
        
        Only respond with the JSON object, no additional text.
        """
        
        # Prepare content for Gemini
        contents = [prompt, image]
        
        # Call Gemini 1.5 Flash for analysis
        response = client.models.generate_content(
            model=analysis_model,
            contents=contents
        )
        
        # Extract text response
        analysis_text = None
        for part in response.candidates[0].content.parts:
            if part.text is not None:
                analysis_text = part.text
                break
        
        if not analysis_text:
            return {
                "error": "No analysis text received from Gemini",
                "is_professional": False,
                "is_single_item": False
            }
        
        # Try to parse JSON response
        try:
            # Clean the response text by removing markdown code blocks
            cleaned_text = analysis_text.strip()
            if cleaned_text.startswith('```json'):
                cleaned_text = cleaned_text[7:]  # Remove ```json
            if cleaned_text.endswith('```'):
                cleaned_text = cleaned_text[:-3]  # Remove ```
            cleaned_text = cleaned_text.strip()
            
            analysis_result = json.loads(cleaned_text)
            return analysis_result
        except json.JSONDecodeError:
            # If JSON parsing fails, return a basic structure
            return {
                "error": "Failed to parse Gemini response as JSON",
                "raw_response": analysis_text,
                "is_professional": False,
                "is_single_item": False
            }
            
    except Exception as e:
        return {
            "error": f"Error analyzing image: {str(e)}",
            "is_professional": False,
            "is_single_item": False
        }

async def identify_clothing_items(image: UploadFile) -> dict:
    """Analyze uploaded image and return a list of clothing items found"""
    processed_image = process_uploaded_image(image)
    return itemize_photo(processed_image)

def itemize_photo(image: Image.Image) -> dict:
    """
    Analyze an image and return a dict of clothing items and accessories found
    
    Args:
        image: PIL Image object to analyze
        
    Returns:
        dict: Dict containing clothing items and accessories found in the image
    """
    client = get_gemini_client()
    
    try:
        # Create analysis prompt
        prompt = """
        Analyze this image and identify all the clothing items visible in the photo.
        
        Please respond with a JSON object containing clothing items and accessories you can clearly identify.
        Use specific, descriptive names for each item (e.g., "blue denim jeans", "white cotton t-shirt", "black leather jacket").
        
        Only include actual clothing items (shirts, pants, dresses, shoes, etc.).
        For accessories like hats, scarves, or bags, include them only if they are clearly visible and part of the outfit. Add them to a separate list.

        Do not include people, backgrounds, or non-clothing objects.
        
        Response format: 
        {"clothing_items": ["item1", "item2", "item3", ...], "accessories": ["accessory1", "accessory2", ...]}
        
        Only respond with the JSON object, no additional text.
        """
        
        # Prepare content for Gemini
        contents = [prompt, image]
        
        # Call Gemini 1.5 Flash for analysis
        response = client.models.generate_content(
            model=analysis_model,
            contents=contents
        )
        
        # Extract text response
        analysis_text = None
        for part in response.candidates[0].content.parts:
            if part.text is not None:
                analysis_text = part.text
                break
        
        if not analysis_text:
            return {"clothing_items": [], "accessories": []}
        
        # Try to parse JSON response
        try:
            # Clean the response text by removing markdown code blocks
            cleaned_text = analysis_text.strip()
            if cleaned_text.startswith('```json'):
                cleaned_text = cleaned_text[7:]  # Remove ```json
            if cleaned_text.endswith('```'):
                cleaned_text = cleaned_text[:-3]  # Remove ```
            cleaned_text = cleaned_text.strip()
            
            response_data = json.loads(cleaned_text)
            
            # Ensure response has the expected structure
            if isinstance(response_data, dict):
                clothing_items = response_data.get("clothing_items", [])
                accessories = response_data.get("accessories", [])
                return {
                    "clothing_items": clothing_items if isinstance(clothing_items, list) else [],
                    "accessories": accessories if isinstance(accessories, list) else []
                }
            
            # Fallback: if response is just a list, treat as clothing items
            if isinstance(response_data, list):
                return {"clothing_items": response_data, "accessories": []}
                
            return {"clothing_items": [], "accessories": []}
                
        except json.JSONDecodeError:
            # If JSON parsing fails, return empty dict
            return {"clothing_items": [], "accessories": []}
            
    except Exception as e:
        # Log error and return empty dict
        print(f"Error itemizing photo: {str(e)}")
        return {"clothing_items": [], "accessories": []}

async def extract_specific_clothing_items(image: UploadFile, clothing_items: str) -> dict:
    """Extract specific clothing items from photo and create professional product images"""
    client = get_gemini_client()
    
    # Process uploaded image
    processed_image = process_uploaded_image(image)
    
    # Parse the clothing items list
    try:
        items_list = json.loads(clothing_items)
        if not isinstance(items_list, list):
            raise ValueError("clothing_items must be a JSON array")
    except json.JSONDecodeError:
        return {
            "success": False,
            "error": "Invalid JSON format for clothing_items"
        }
    
    if not items_list:
        return {
            "success": False,
            "error": "No clothing items specified"
        }
    
    extracted_images = []
    
    # Loop through each clothing item and extract it
    for item in items_list:
        try:
            # Create the extraction prompt for specific item
            prompt = f"Take the {item} in this photo and make a full view image of just that item with a white background as a professionally shot image for a clothing item on an online store. Focus only on the {item} and exclude all other clothing items or objects. Do not change any details from the clothes. Be as accurate as possible."

            # Prepare content for Gemini
            contents = [prompt, processed_image]
            
            # Generate the professional product image
            response = client.models.generate_content(
                model=editing_model,
                contents=contents
            )
            
            # Process response - check for both generated image and text description
            generated_image_base64 = None
            description_text = None
            
            for part in response.candidates[0].content.parts:
                if part.text is not None:
                    description_text = part.text
                elif part.inline_data is not None:
                    image_data = Image.open(io.BytesIO(part.inline_data.data))
                    generated_image_base64 = image_to_base64(image_data)
            
            # Add to results
            extracted_images.append({
                "item": item,
                "success": True,
                "generated_image_base64": generated_image_base64,
                "description": description_text if description_text else f"Professional {item} product image generated"
            })
            
        except Exception as item_error:
            # If extraction fails for this item, add error to results
            extracted_images.append({
                "item": item,
                "success": False,
                "error": f"Error extracting {item}: {str(item_error)}",
                "generated_image_base64": None,
                "description": None
            })
    
    # Count successful extractions
    successful_extractions = sum(1 for result in extracted_images if result["success"])
    
    return {
        "success": True,
        "extracted_images": extracted_images,
        "total_items": len(items_list),
        "successful_extractions": successful_extractions,
        "filename": image.filename
    }

async def extract_specific_clothing_items_batch(image: UploadFile, clothing_items: str) -> dict:
    """Extract specific clothing items from photo using batch mode for efficiency"""
    client = get_gemini_client()
    
    # Process uploaded image
    processed_image = process_uploaded_image(image)
    
    # Parse the clothing items list
    try:
        items_list = json.loads(clothing_items)
        if not isinstance(items_list, list):
            raise ValueError("clothing_items must be a JSON array")
    except json.JSONDecodeError:
        return {
            "success": False,
            "error": "Invalid JSON format for clothing_items"
        }
    
    if not items_list:
        return {
            "success": False,
            "error": "No clothing items specified"
        }
    
    try:
        # Convert processed image to base64 for batch requests
        if hasattr(processed_image, 'data'):
            # If it's already inline data
            image_base64 = base64.b64encode(processed_image.data).decode('utf-8')
            mime_type = processed_image.mime_type
        else:
            # If it's a PIL Image, convert it
            buffer = io.BytesIO()
            processed_image.save(buffer, format='PNG')
            image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
            mime_type = 'image/png'
        
        # Create batch requests for all clothing items
        batch_requests = []
        for i, item in enumerate(items_list):
            prompt = f"Take the {item} in this photo and make a full view image of just that item with a white background as a professionally shot image for a clothing item on an online store. Focus only on the {item} and exclude all other clothing items or objects."
            
            request = {
                'contents': [{
                    'parts': [
                        {'text': prompt},
                        {
                            'inline_data': {
                                'mime_type': mime_type,
                                'data': image_base64
                            }
                        }
                    ],
                    'role': 'user'
                }]
            }
            
            batch_requests.append(request)
        
        # Create and submit batch job
        batch_job = client.batches.create(
            model="gemini-2.5-flash-image-preview",
            src=batch_requests,
            config={
                'display_name': f"clothing-extraction-{int(time.time())}"
            }
        )
        
        print(f"Created batch job: {batch_job.name}")
        
        # Poll for completion
        max_wait_time = 1800  # 30 minutes max wait
        poll_interval = 10    # Check every 10 seconds
        elapsed_time = 0
        
        completed_states = {'JOB_STATE_SUCCEEDED', 'JOB_STATE_FAILED', 'JOB_STATE_CANCELLED'}
        
        while elapsed_time < max_wait_time:
            current_job = client.batches.get(name=batch_job.name)
            print(f"Job status: {current_job.state.name} (elapsed: {elapsed_time}s)")
            
            if current_job.state.name in completed_states:
                break
                
            time.sleep(poll_interval)
            elapsed_time += poll_interval
        
        # Check final job status
        final_job = client.batches.get(name=batch_job.name)
        
        if final_job.state.name != 'JOB_STATE_SUCCEEDED':
            return {
                "success": False,
                "error": f"Batch job failed with status: {final_job.state.name}",
                "job_error": str(final_job.error) if hasattr(final_job, 'error') else None
            }
        
        # Process results
        extracted_images = []
        
        if final_job.dest and final_job.dest.inlined_responses:
            # Process inline responses
            for i, inline_response in enumerate(final_job.dest.inlined_responses):
                item = items_list[i] if i < len(items_list) else f"item_{i}"
                
                if inline_response.response:
                    try:
                        # Extract generated image and description
                        generated_image_base64 = None
                        description_text = None
                        
                        for part in inline_response.response.candidates[0].content.parts:
                            if hasattr(part, 'text') and part.text:
                                description_text = part.text
                            elif hasattr(part, 'inline_data') and part.inline_data:
                                # Convert image data to base64
                                image_data = Image.open(io.BytesIO(part.inline_data.data))
                                generated_image_base64 = image_to_base64(image_data)
                        
                        extracted_images.append({
                            "item": item,
                            "success": True,
                            "generated_image_base64": generated_image_base64,
                            "description": description_text if description_text else f"Professional {item} product image generated"
                        })
                        
                    except Exception as process_error:
                        extracted_images.append({
                            "item": item,
                            "success": False,
                            "error": f"Error processing response for {item}: {str(process_error)}",
                            "generated_image_base64": None,
                            "description": None
                        })
                
                elif inline_response.error:
                    extracted_images.append({
                        "item": item,
                        "success": False,
                        "error": f"Batch processing error for {item}: {str(inline_response.error)}",
                        "generated_image_base64": None,
                        "description": None
                    })
        
        else:
            return {
                "success": False,
                "error": "No results found in batch response"
            }
        
        # Count successful extractions
        successful_extractions = sum(1 for result in extracted_images if result["success"])
        
        return {
            "success": True,
            "extracted_images": extracted_images,
            "total_items": len(items_list),
            "successful_extractions": successful_extractions,
            "filename": image.filename,
            "batch_job_id": batch_job.name,
            "processing_time": elapsed_time
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Batch processing failed: {str(e)}"
        }

async def extract_specific_clothing_items_batch_file(image: UploadFile, clothing_items: str) -> dict:
    """Extract specific clothing items using file-based batch mode for large requests"""
    client = get_gemini_client()
    
    # Process uploaded image and upload to File API
    processed_image = process_uploaded_image(image)
    
    # Upload image to File API for reuse across batch requests
    if hasattr(processed_image, 'data'):
        # Create temporary file from inline data
        temp_filename = f"temp_image_{int(time.time())}.png"
        with open(temp_filename, 'wb') as f:
            f.write(processed_image.data)
        
        uploaded_image = client.files.upload(
            file=temp_filename,
            config=types.UploadFileConfig(
                display_name=f'clothing_image_{int(time.time())}',
                mime_type=processed_image.mime_type
            )
        )
        
        # Clean up temp file
        os.remove(temp_filename)
    else:
        # Save PIL Image and upload
        temp_filename = f"temp_image_{int(time.time())}.png"
        processed_image.save(temp_filename)
        
        uploaded_image = client.files.upload(
            file=temp_filename,
            config=types.UploadFileConfig(
                display_name=f'clothing_image_{int(time.time())}',
                mime_type='image/png'
            )
        )
        
        # Clean up temp file
        os.remove(temp_filename)
    
    # Parse clothing items
    try:
        items_list = json.loads(clothing_items)
        if not isinstance(items_list, list):
            raise ValueError("clothing_items must be a JSON array")
    except json.JSONDecodeError:
        return {"success": False, "error": "Invalid JSON format for clothing_items"}
    
    if not items_list:
        return {"success": False, "error": "No clothing items specified"}
    
    # Create JSONL file with batch requests
    jsonl_filename = f"clothing_batch_{int(time.time())}.jsonl"
    
    with open(jsonl_filename, "w") as f:
        for i, item in enumerate(items_list):
            prompt = f"Take the {item} in this photo and make a full view image of just that item with a white background as a professionally shot image for a clothing item on an online store. Focus only on the {item} and exclude all other clothing items or objects."
            
            request_data = {
                "key": f"item_{i}_{item}",
                "request": {
                    "contents": [{
                        "parts": [
                            {"text": prompt},
                            {"file_data": {"file_uri": uploaded_image.uri}}
                        ]
                    }]
                }
            }
            
            f.write(json.dumps(request_data) + "\n")
    
    # Upload JSONL file
    batch_input_file = client.files.upload(
        file=jsonl_filename,
        config=types.UploadFileConfig(
            display_name=f'clothing_batch_input_{int(time.time())}',
            mime_type='application/jsonl'
        )
    )
    
    # Clean up local JSONL file
    os.remove(jsonl_filename)
    
    # Create batch job
    batch_job = client.batches.create(
        model="gemini-2.5-flash-image-preview",
        src=batch_input_file.name,
        config={
            'display_name': f"clothing-extraction-file-{int(time.time())}"
        }
    )
    
    # Return job information for async processing
    return {
        "success": True,
        "batch_job_id": batch_job.name,
        "status": "submitted",
        "message": "Batch job submitted. Use check_batch_status() to monitor progress.",
        "total_items": len(items_list),
        "filename": image.filename
    }

def check_batch_status(batch_job_id: str) -> dict:
    """Check the status of a batch job and retrieve results if completed"""
    client = get_gemini_client()
    
    try:
        batch_job = client.batches.get(name=batch_job_id)
        
        if batch_job.state.name == 'JOB_STATE_SUCCEEDED':
            # Download and process results
            if batch_job.dest and batch_job.dest.file_name:
                result_file_name = batch_job.dest.file_name
                file_content = client.files.download(file=result_file_name)
                
                extracted_images = []
                
                for line in file_content.decode('utf-8').splitlines():
                    if line.strip():
                        result = json.loads(line)
                        
                        # Extract item name from key
                        item_key = result.get('key', 'unknown')
                        item_name = item_key.split('_', 2)[-1] if '_' in item_key else item_key
                        
                        if 'response' in result:
                            response = result['response']
                            generated_image_base64 = None
                            description_text = None
                            
                            # Process response parts
                            candidates = response.get('candidates', [])
                            if candidates and 'content' in candidates[0]:
                                parts = candidates[0]['content'].get('parts', [])
                                
                                for part in parts:
                                    if 'text' in part and part['text']:
                                        description_text = part['text']
                                    elif 'inlineData' in part and part['inlineData']:
                                        # Convert to base64
                                        image_data = base64.b64decode(part['inlineData']['data'])
                                        image = Image.open(io.BytesIO(image_data))
                                        generated_image_base64 = image_to_base64(image)
                            
                            extracted_images.append({
                                "item": item_name,
                                "success": True,
                                "generated_image_base64": generated_image_base64,
                                "description": description_text or f"Professional {item_name} product image generated"
                            })
                        
                        elif 'error' in result:
                            extracted_images.append({
                                "item": item_name,
                                "success": False,
                                "error": str(result['error']),
                                "generated_image_base64": None,
                                "description": None
                            })
                
                successful_extractions = sum(1 for result in extracted_images if result["success"])
                
                return {
                    "success": True,
                    "status": "completed",
                    "extracted_images": extracted_images,
                    "total_items": len(extracted_images),
                    "successful_extractions": successful_extractions
                }
            
        elif batch_job.state.name == 'JOB_STATE_FAILED':
            return {
                "success": False,
                "status": "failed",
                "error": str(batch_job.error) if hasattr(batch_job, 'error') else "Unknown error"
            }
        
        elif batch_job.state.name == 'JOB_STATE_CANCELLED':
            return {
                "success": False,
                "status": "cancelled"
            }
        
        else:
            return {
                "success": True,
                "status": "pending",
                "current_state": batch_job.state.name,
                "message": "Job is still processing..."
            }
            
    except Exception as e:
        return {
            "success": False,
            "status": "error",
            "error": f"Error checking batch status: {str(e)}"
        }

async def extract_specific_clothing_items_concurrent(image: UploadFile, clothing_items: str) -> dict:
    """Extract specific clothing items from photo using concurrent async requests for better performance"""
    client = get_gemini_client()
    
    # Process uploaded image
    processed_image = process_uploaded_image(image)
    
    # Parse the clothing items list
    try:
        items_list = json.loads(clothing_items)
        if not isinstance(items_list, list):
            raise ValueError("clothing_items must be a JSON array")
    except json.JSONDecodeError:
        return {
            "success": False,
            "error": "Invalid JSON format for clothing_items"
        }
    
    if not items_list:
        return {
            "success": False,
            "error": "No clothing items specified"
        }
    
    # Send all requests concurrently using async Gemini client
    start_time = time.time()
    print(f"Sending {len(items_list)} concurrent async requests...")
    
    # Create async tasks for all items - these will all be sent simultaneously
    tasks = []
    for item in items_list:
        # Create the extraction prompt for specific item
        prompt = f"Take the {item} in this photo and make a full view image of just that item with a white background as a professionally shot image for a clothing item on an online store. Focus only on the {item} and exclude all other clothing items or objects. Do not change any details from the clothes. Be as accurate as possible."
        
        # Prepare content for Gemini
        contents = [prompt, processed_image]
        
        # Create async task using aio client - this doesn't execute yet
        task = client.aio.models.generate_content(
            model=editing_model,
            contents=contents
        )
        tasks.append((item, task))
    
    # Execute all requests concurrently and wait for all to complete
    try:
        # Extract just the tasks for asyncio.gather
        async_tasks = [task for _, task in tasks]
        responses = await asyncio.gather(*async_tasks, return_exceptions=True)
        
        requests_completed_time = time.time() - start_time
        print(f"All {len(items_list)} async requests completed in {requests_completed_time:.2f}s")
        
        # Process all responses
        extracted_images = []
        for i, (item, _) in enumerate(tasks):
            response = responses[i]
            
            if isinstance(response, Exception):
                extracted_images.append({
                    "item": item,
                    "success": False,
                    "error": f"Request exception for {item}: {str(response)}",
                    "generated_image_base64": None,
                    "description": None
                })
                continue
            
            # Process successful response
            try:
                generated_image_base64 = None
                description_text = None
                
                for part in response.candidates[0].content.parts:
                    if part.text is not None:
                        description_text = part.text
                    elif part.inline_data is not None:
                        image_data = Image.open(io.BytesIO(part.inline_data.data))
                        padded_image = image_utils.pad_image_to_square(image_data)
                        generated_image_base64 = image_to_base64(padded_image)
                
                extracted_images.append({
                    "item": item,
                    "success": True,
                    "generated_image_base64": generated_image_base64,
                    "description": description_text if description_text else f"Professional {item} product image generated"
                })
                
            except Exception as process_error:
                extracted_images.append({
                    "item": item,
                    "success": False,
                    "error": f"Error processing response for {item}: {str(process_error)}",
                    "generated_image_base64": None,
                    "description": None
                })
        
    except Exception as e:
        print(f"Error in concurrent processing: {str(e)}")
        # Fallback to error responses for all items
        extracted_images = []
        for item in items_list:
            extracted_images.append({
                "item": item,
                "success": False,
                "error": f"Concurrent processing failed: {str(e)}",
                "generated_image_base64": None,
                "description": None
            })
    
    processing_time = time.time() - start_time
    
    # Count successful extractions
    successful_extractions = sum(1 for result in extracted_images if result["success"])
    
    return {
        "success": True,
        "extracted_images": extracted_images,
        "total_items": len(items_list),
        "successful_extractions": successful_extractions,
        "filename": image.filename,
        "processing_time": round(processing_time, 2),
        "processing_method": "concurrent_async"
    }
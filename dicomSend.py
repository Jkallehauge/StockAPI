from pydicom import dcmread
from pynetdicom import AE
import os
from pynetdicom.sop_class import CTImageStorage, MRImageStorage, Verification
from pynetdicom import AE, ALL_TRANSFER_SYNTAXES
import tkinter as tk
from tkinter import filedialog
# Load the DICOM file you want to send
#dicom_file_path = 'C:\StockAPI\\test\Riget_test'
# Open the folder dialog
dicom_file_path = filedialog.askdirectory()
#dicom_file_path = 'C:\StockAPI\\in_hn'

#dicom_dataset = dcmread(dicom_file_path)

# Create an Application Entity (AE) for the DICOM client

destination_aet = 'DL_pipe'
destination_ip = 'dcpt-frog2.onerm.dk'
destination_port = 11113  # Default DICOM port
ae = AE(ae_title='DL_Pipe')


# Add a DICOM Verification SOP Class (required for association negotiation)
ae.add_requested_context(CTImageStorage, ALL_TRANSFER_SYNTAXES)
ae.add_requested_context(MRImageStorage, ALL_TRANSFER_SYNTAXES)
ae.add_requested_context('1.2.840.10008.5.1.4.1.1.481.3', ALL_TRANSFER_SYNTAXES)
ae.add_requested_context('1.2.840.10008.5.1.4.1.1.11.1', ALL_TRANSFER_SYNTAXES)


# Create a DICOM association with the destination AE
assoc = ae.associate(destination_ip, destination_port, ae_title=destination_aet)

if assoc.is_established:
    print("Association established.")

    for dcm_file in os.scandir(dicom_file_path):        
    # Read the DICOM file

        dicom_dataset = dcmread(dcm_file)

        # Send the DICOM dataset
        status = assoc.send_c_store(dicom_dataset)

        if status:
            print(f"DICOM file sent successfully with status:")
        else:
            print("Failed to send DICOM file.")

    # Release the association
    assoc.release()
else:
    print("Association rejected, aborted, or failed to establish.")

